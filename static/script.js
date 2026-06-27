const trainButton = document.getElementById('trainButton');
let currentTreeNodes = [];

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = value;
    }
}

function show(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.remove('hidden');
    }
}

function hide(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.add('hidden');
    }
}

function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

function renderTable(tableId, rows) {
    const table = document.getElementById(tableId);

    if (!table || !rows || rows.length === 0) {
        return;
    }

    const columns = Object.keys(rows[0]);

    table.innerHTML = `
        <thead>
            <tr>
                ${columns.map(column => `<th>${escapeHtml(column)}</th>`).join('')}
            </tr>
        </thead>
        <tbody>
            ${rows.map(row => `
                <tr>
                    ${columns.map(column => `<td>${escapeHtml(row[column])}</td>`).join('')}
                </tr>
            `).join('')}
        </tbody>
    `;
}

function renderTestTable(rows) {
    const table = document.getElementById('testTable');

    if (!table || !rows || rows.length === 0) {
        return;
    }

    table.innerHTML = `
        <thead>
            <tr>
                <th>№</th>
                <th>Прогноз дерева</th>
                <th>Реальный тип</th>
                <th>Результат</th>
            </tr>
        </thead>
        <tbody>
            ${rows.map(row => `
                <tr>
                    <td>${escapeHtml(row.number)}</td>
                    <td>${escapeHtml(row.prediction)}</td>
                    <td>${escapeHtml(row.real)}</td>
                    <td class="${row.correct ? 'good' : 'bad'}">${escapeHtml(row.result)}</td>
                </tr>
            `).join('')}
        </tbody>
    `;
}

function renderTree(nodes) {
    const canvas = document.getElementById('treeCanvas');
    const details = document.getElementById('nodeDetails');

    if (!canvas || !nodes || nodes.length === 0 || !nodes[0]) {
        return;
    }

    currentTreeNodes = nodes;
    const existingNodes = nodes.filter(Boolean);
    const maxDepth = Math.max(...existingNodes.map(node => node.depth));
    const levelHtml = [];

    for (let depth = 0; depth <= maxDepth; depth += 1) {
        const startIndex = Math.pow(2, depth) - 1;
        const levelSize = Math.pow(2, depth);
        const slots = [];

        for (let position = 0; position < levelSize; position += 1) {
            const node = nodes[startIndex + position];

            if (!node) {
                slots.push('<div class="tree-slot tree-slot-empty"></div>');
                continue;
            }

            const branchClass = node.branch === 'Да'
                ? 'branch-yes'
                : node.branch === 'Нет'
                    ? 'branch-no'
                    : 'branch-root';

            const nodeType = node.is_leaf ? 'Лист' : 'Узел';

            slots.push(`
                <button class="compact-node ${branchClass}" data-node-index="${node.index}" type="button">
                    <span class="compact-depth">Глубина ${escapeHtml(node.depth)}</span>
                    <strong>${escapeHtml(node.branch)}</strong>
                    <em>${nodeType}</em>
                </button>
            `);
        }

        levelHtml.push(`
            <div class="tree-level level-${depth}" style="grid-template-columns: repeat(${levelSize}, minmax(120px, 1fr));">
                ${slots.join('')}
            </div>
        `);
    }

    canvas.innerHTML = levelHtml.join('');

    canvas.querySelectorAll('.compact-node').forEach(button => {
        button.addEventListener('click', () => {
            const nodeIndex = Number(button.dataset.nodeIndex);
            const node = currentTreeNodes[nodeIndex];

            canvas.querySelectorAll('.compact-node').forEach(item => item.classList.remove('active'));
            button.classList.add('active');

            renderNodeDetails(node);
        });
    });

    if (details) {
        details.innerHTML = 'Нажмите на любой блок дерева, чтобы посмотреть энтропию, вопрос и состав объектов.';
    }
}

function renderNodeDetails(node) {
    const details = document.getElementById('nodeDetails');

    if (!details || !node) {
        return;
    }

    const objectsHtml = node.objects.map(item => `
        <div class="detail-object-row">
            <span>${escapeHtml(item.name)}</span>
            <strong>${escapeHtml(item.count)}</strong>
        </div>
    `).join('');

    const questionHtml = node.question
        ? `<div class="detail-line"><span>Вопрос</span><strong>${escapeHtml(node.question)}?</strong></div>`
        : '<div class="detail-line"><span>Вопрос</span><strong>Вопроса нет, это конечный лист</strong></div>';

    const resultHtml = node.is_leaf
        ? `<div class="detail-result">Итоговый класс: ${escapeHtml(node.prediction)}</div>`
        : '<div class="detail-result neutral">Узел продолжает деление</div>';

    details.innerHTML = `
        <div class="detail-head">
            <div>
                <span>Выбранный блок</span>
                <h3>Глубина ${escapeHtml(node.depth)} · ${escapeHtml(node.branch)}</h3>
            </div>
        </div>

        <div class="detail-grid">
            <div class="detail-line">
                <span>Энтропия</span>
                <strong>${escapeHtml(node.entropy)}</strong>
            </div>
            <div class="detail-line">
                <span>Объектов в блоке</span>
                <strong>${escapeHtml(node.object_count)}</strong>
            </div>
            ${questionHtml}
        </div>

        <div class="detail-objects">
            <h4>Объекты в блоке</h4>
            ${objectsHtml}
        </div>

        ${resultHtml}
    `;
}

function resetSections() {
    hide('warning');
    hide('resultSection');
    hide('treeSection');
    hide('previewSection');
    hide('testSection');
}

if (trainButton) {
    trainButton.addEventListener('click', async () => {
        const warning = document.getElementById('warning');

        trainButton.disabled = true;
        resetSections();
        setText('status', 'Идёт обучение дерева решений...');

        try {
            const response = await fetch('/api/train', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (!data.success) {
                throw new Error(data.details || data.error || 'Неизвестная ошибка');
            }

            setText('status', 'Готово. Обучение завершено. Нажмите на блок дерева, чтобы увидеть подробности.');
            setText('depthResult', data.depth);
            setText('accuracyResult', `${data.accuracy_text} (${data.accuracy_percent})`);
            setText('correctResult', `${data.correct_count} из ${data.test_count}`);
            setText('datasetRowsResult', data.dataset_rows);
            setText('trainRowsResult', data.train_rows);
            setText('testRowsResult', data.test_rows_count);

            renderTree(data.tree_nodes);
            renderTable('previewTable', data.preview);
            renderTestTable(data.test_rows);

            show('resultSection');
            show('treeSection');
            show('previewSection');
            show('testSection');
        } catch (error) {
            setText('status', 'Ошибка. Обучение не выполнено.');
            warning.textContent = error.message;
            show('warning');
        } finally {
            trainButton.disabled = false;
        }
    });
}
